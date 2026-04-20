#include <AccelStepper.h>
#include <math.h>

// ============================================================
// PINS
// ============================================================
constexpr uint8_t STEP_PIN = 25;
constexpr uint8_t DIR_PIN  = 26;
constexpr uint8_t EN_PIN   = 27;

constexpr uint8_t ENC_A = 34;   // encoder A, white
constexpr uint8_t ENC_B = 35;   // encoder B, green

// ============================================================
// WAVE SIMULATION KNOBS
// You can tune these later without touching the control logic.
// ============================================================

// Main wave speed (Hz). Period in seconds = 1 / WAVE_HZ
// Overnight test was stable, so this pushes harder.
constexpr float WAVE_HZ = 0.18f;                 // about 5.6 s per cycle

// Main travel (encoder counts). This is your "amplitude".
// Increase carefully, it raises peak speed and load.
constexpr long AMP_COUNTS = 950;                 // bigger wave travel

// Adds choppiness by blending a faster harmonic on top of the swell.
// 0.0 = pure sine, 0.1 to 0.35 looks wave-like.
constexpr float CHOP_RATIO = 0.22f;              // 22% of swell amplitude
constexpr int   CHOP_HARMONIC = 3;               // 2 or 3 works well
constexpr float CHOP_PHASE_RAD = 0.9f;           // phase offset for the chop

// "Sets" are slow changes in overall height, like groups of waves.
// 0.0 disables. Try 0.01 to 0.03 Hz.
constexpr float SET_HZ = 0.015f;                 // about 66 s per set
constexpr float SET_DEPTH = 0.18f;               // 18% amplitude modulation

// ============================================================
// MOTOR CAPABILITY (must be high enough to keep up)
// ============================================================
constexpr float MAX_SPEED_STEPS = 3200.0f;       // steps per second
constexpr float ACCEL_STEPS     = 5200.0f;       // steps per second^2

// ============================================================
// CLOSED LOOP CONTROL
// ============================================================
// Proportional tracking. Higher follows better, too high can hunt.
constexpr float KP_TRACK = 0.35f;                // 0.25 to 0.50 typical

// Drift lock. Slow integral correction near peaks only.
constexpr float KI_RECENTER = 0.02f;             // 0.01 to 0.05 typical

// Peak window. Smaller means only correct at very top and bottom.
constexpr float PEAK_WINDOW_COS = 0.10f;
constexpr float PEAK_SIN_THRESH = 0.985f;

// Clamp corrections so nothing can run away.
constexpr float PCORR_CLAMP_STEPS = 900.0f;
constexpr long  OFFSET_CLAMP_STEPS = 4000;

// ============================================================
// SAFETY
// ============================================================
// Soft travel limit around the start center position in encoder counts.
// This must be larger than your true motion range.
// If you increase AMP_COUNTS, increase SOFT_LIMIT_COUNTS too.
constexpr long SOFT_LIMIT_COUNTS = 2600;

// Guard margin so we never intentionally command near the soft limit.
constexpr long SOFT_GUARD_COUNTS = 150;

// Encoder stall detection
constexpr uint32_t SAMPLE_MS = 50;
constexpr uint32_t STALL_MS  = 1400;
constexpr long MIN_DTG_FOR_STALL = 250;

// Debug prints
constexpr bool DEBUG_PRINTS = true;
constexpr uint32_t PRINT_MS = 500;

// ============================================================
// ENCODER DECODE
// ============================================================
volatile long encCount = 0;
portMUX_TYPE encMux = portMUX_INITIALIZER_UNLOCKED;
volatile uint8_t lastAB = 0;

const int8_t QDEC[16] = {
  0, -1, +1,  0,
 +1,  0,  0, -1,
 -1,  0,  0, +1,
  0, +1, -1,  0
};

inline uint8_t readAB() {
  uint8_t a = (uint8_t)digitalRead(ENC_A);
  uint8_t b = (uint8_t)digitalRead(ENC_B);
  return (a << 1) | b;
}

void IRAM_ATTR onEncChange() {
  uint8_t ab = readAB();
  uint8_t idx = (lastAB << 2) | ab;
  int8_t delta = QDEC[idx];
  lastAB = ab;

  if (delta != 0) {
    portENTER_CRITICAL_ISR(&encMux);
    encCount += delta;
    portEXIT_CRITICAL_ISR(&encMux);
  }
}

long getEncCount() {
  portENTER_CRITICAL(&encMux);
  long c = encCount;
  portEXIT_CRITICAL(&encMux);
  return c;
}

// ============================================================
// STEPPER
// ============================================================
AccelStepper motor(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

// Calibration results
float countsPerStep = 0.0f;   // encoder counts per motor step, sign included
long  encZero = 0;            // encoder count center, where the wave is anchored

// Drift lock state
float offsetSteps = 0.0f;
bool topLatched = false;
bool botLatched = false;

// ============================================================
// HELPERS
// ============================================================
void hardStop(const char* msg) {
  if (DEBUG_PRINTS) Serial.println(msg);
  motor.stop();
  while (motor.isRunning()) motor.run();
  while (true) delay(1000);
}

float clampf(float v, float lo, float hi) {
  if (v < lo) return lo;
  if (v > hi) return hi;
  return v;
}

// Realistic wave shape, returns desired offset in encoder counts from center.
long waveOffsetCounts(float phase, float tSec) {
  float s1 = sinf(phase);

  float sChop = 0.0f;
  if (CHOP_RATIO > 0.0f) {
    sChop = sinf((float)CHOP_HARMONIC * phase + CHOP_PHASE_RAD);
  }

  float setMod = 1.0f;
  if (SET_HZ > 0.0f && SET_DEPTH > 0.0f) {
    setMod = 1.0f + SET_DEPTH * sinf(2.0f * 3.1415926f * SET_HZ * tSec);
    setMod = clampf(setMod, 1.0f - SET_DEPTH, 1.0f + SET_DEPTH);
  }

  float wave = (float)AMP_COUNTS * setMod * (s1 + CHOP_RATIO * sChop);

  // Keep within soft guard by clamping desired command.
  float maxAllowed = (float)(SOFT_LIMIT_COUNTS - SOFT_GUARD_COUNTS);
  wave = clampf(wave, -maxAllowed, +maxAllowed);

  return (long)lroundf(wave);
}

// ============================================================
// SETUP
// ============================================================
constexpr long CAL_STEPS = 1500;

void setup() {
  if (DEBUG_PRINTS) {
    Serial.begin(115200);
    delay(300);
  }

  pinMode(EN_PIN, OUTPUT);
  digitalWrite(EN_PIN, LOW); // enable DM542

  pinMode(ENC_A, INPUT);     // external pullups to 3.3V already installed
  pinMode(ENC_B, INPUT);

  lastAB = readAB();
  attachInterrupt(digitalPinToInterrupt(ENC_A), onEncChange, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENC_B), onEncChange, CHANGE);

  motor.setMaxSpeed(MAX_SPEED_STEPS);
  motor.setAcceleration(ACCEL_STEPS);

  if (DEBUG_PRINTS) Serial.println("Calibration move, forward and back.");

  long c0 = getEncCount();

  motor.setCurrentPosition(0);
  motor.moveTo(+CAL_STEPS);
  while (motor.distanceToGo() != 0) motor.run();

  long c1 = getEncCount();

  motor.moveTo(0);
  while (motor.distanceToGo() != 0) motor.run();

  long dCounts = c1 - c0;

  if (DEBUG_PRINTS) {
    Serial.print("Calibration deltaCounts=");
    Serial.println(dCounts);
  }

  if (labs(dCounts) < 50) {
    hardStop("ERROR: Encoder not counting, check pullups, ground, coupling.");
  }

  countsPerStep = (float)dCounts / (float)CAL_STEPS;
  encZero = getEncCount();

  motor.setCurrentPosition(0);
  offsetSteps = 0.0f;

  if (DEBUG_PRINTS) {
    Serial.print("countsPerStep=");
    Serial.println(countsPerStep, 6);
    Serial.print("encZero=");
    Serial.println(encZero);
    Serial.println("Starting wave simulation.");
  }
}

// ============================================================
// LOOP
// ============================================================
void loop() {
  uint32_t nowMs = millis();
  float tSec = nowMs / 1000.0f;

  long encNow = getEncCount();

  // Safety stop if we ever drift too far from center.
  if (labs(encNow - encZero) > SOFT_LIMIT_COUNTS) {
    hardStop("SOFT LIMIT HIT: encoder moved too far from center, stopping.");
  }

  // Phase, offset so motion starts immediately
  float phase = 2.0f * 3.1415926f * WAVE_HZ * tSec + 3.1415926f / 2.0f;
  float s = sinf(phase);
  float c = cosf(phase);

  // Desired absolute position in encoder counts
  long desiredAbsCounts = encZero + waveOffsetCounts(phase, tSec);

  // Convert desired encoder position to desired motor steps (relative)
  float desiredStepsF = (float)(desiredAbsCounts - encZero) / countsPerStep;

  // Actual position in motor steps from encoder truth
  float actualStepsF = (float)(encNow - encZero) / countsPerStep;

  // Error between desired and actual
  float errStepsF = desiredStepsF - actualStepsF;

  // Proportional tracking help
  float pCorr = KP_TRACK * errStepsF;
  pCorr = clampf(pCorr, -PCORR_CLAMP_STEPS, +PCORR_CLAMP_STEPS);

  // Drift lock near peaks only
  bool nearPeak = (fabsf(c) < PEAK_WINDOW_COS);
  bool nearTop  = nearPeak && (s >  PEAK_SIN_THRESH);
  bool nearBot  = nearPeak && (s < -PEAK_SIN_THRESH);

  if (nearTop && !topLatched) {
    topLatched = true;
    offsetSteps += KI_RECENTER * errStepsF;
  }
  if (!nearTop) topLatched = false;

  if (nearBot && !botLatched) {
    botLatched = true;
    offsetSteps += KI_RECENTER * errStepsF;
  }
  if (!nearBot) botLatched = false;

  // Clamp offset so it cannot run away
  offsetSteps = clampf(offsetSteps, (float)-OFFSET_CLAMP_STEPS, (float)+OFFSET_CLAMP_STEPS);

  // Final target
  long targetSteps = (long)lroundf(desiredStepsF + offsetSteps + pCorr);

  motor.moveTo(targetSteps);
  motor.run();

  // Encoder stall detection, motor commanded but encoder not changing
  static uint32_t lastSampleMs = 0;
  static long lastEnc = 0;
  static uint32_t lastEncMoveMs = 0;

  if (nowMs - lastSampleMs >= SAMPLE_MS) {
    lastSampleMs = nowMs;

    long d = encNow - lastEnc;
    lastEnc = encNow;
    if (d != 0) lastEncMoveMs = nowMs;

    if (labs(motor.distanceToGo()) > MIN_DTG_FOR_STALL) {
      if (nowMs - lastEncMoveMs > STALL_MS) {
        hardStop("STALL: motor commanded but encoder not changing, stopping.");
      }
    }
  }

  // Debug prints
  if (DEBUG_PRINTS) {
    static uint32_t lastPrintMs = 0;
    if (nowMs - lastPrintMs > PRINT_MS) {
      lastPrintMs = nowMs;
      Serial.print("enc=");
      Serial.print(encNow);
      Serial.print(" desAbs=");
      Serial.print(desiredAbsCounts);
      Serial.print(" errSteps=");
      Serial.print(errStepsF, 2);
      Serial.print(" offsetSteps=");
      Serial.print(offsetSteps, 2);
      Serial.print(" tgt=");
      Serial.print(targetSteps);
      Serial.print(" dtg=");
      Serial.println(motor.distanceToGo());
    }
  }
}
