#include <AFMotor.h>

// 右輪用 Motor 2、左輪用 Motor 1
AF_DCMotor motorRight(2);
AF_DCMotor motorLeft(1);

void setup() {
  Serial.begin(9600);
  motorRight.setSpeed(0);
  motorLeft.setSpeed(0);
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    int commaIndex = line.indexOf(',');
    if (commaIndex > 0) {
      int pwmR = line.substring(0, commaIndex).toInt();
      int pwmL = line.substring(commaIndex + 1).toInt();

      pwmR = constrain(pwmR, -255, 255);
      pwmL = constrain(pwmL, -255, 255);

      // 右輪方向與速度
      motorRight.setSpeed(abs(pwmR));
      motorRight.run(pwmR >= 0 ? FORWARD : BACKWARD);

      // 左輪方向與速度
      motorLeft.setSpeed(abs(pwmL));
      motorLeft.run(pwmL >= 0 ? FORWARD : BACKWARD);

      // Debug output
      Serial.print("R: "); Serial.print(pwmR);
      Serial.print(" L: "); Serial.println(pwmL);
    }
  }
}
