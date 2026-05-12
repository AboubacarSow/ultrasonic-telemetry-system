long duration;
int distance;

const int triggerPing = 13;
const int echoPing = 12;

void setup() {
  pinMode(triggerPing, OUTPUT);
  pinMode(echoPing, INPUT);
  Serial.begin(9600);
  delay(2000);
}

void loop() {
  // Ensure trigger is LOW before pulse
  digitalWrite(triggerPing, LOW);
  delayMicroseconds(5);  // slightly longer LOW settle

  // Send 10µs HIGH pulse
  digitalWrite(triggerPing, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPing, LOW);

  duration = pulseIn(echoPing, HIGH, 30000);

  // Detect timeout (pulseIn returns 0 on timeout)
  if (duration == 0) {
    Serial.println(-1);
  } else {
    distance = (duration * 0.034) / 2;
    Serial.println(distance);
  }

  delay(100);  
}