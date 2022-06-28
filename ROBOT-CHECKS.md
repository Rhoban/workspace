# Checking that a robot is OK

## Zero and legs backlash

- Set the robot to `init` and check for misalignments and important backlashes

## Check piano wires

- They should not be bent, head should not hit the ground when the robot fall

## Camera focus check

- Check that the camera focus is not blurry with `view /Vision/TaggedImg`.

## Horizon line check

- Run `view /Vision/TaggedImg`, check that the (blue) horizon line is properly positionned.
  You can have a look at a goal post, the horizon line should be at the same height that the robot if it was there.

## Perception check

- Run `view /Vision/yolo/out`, check that the objects are well detected.

## Ball position check

- Run `init`, `walk` and `/moves/head/disabled=0`, put a ball at robot's feet, it should watch it.
  Center the ball in front of the robot, check for:
  - `/localisation/ballY`: should be 0
  - `/localisation/ballX`: should be ~0.2

## Standup check

- Check that the robot is able to standup front and back side.

# Kick check

- Run the left and right foot kick for each possible kicks (`classic`, `lateral` and `small`).

## IMU check

- Run the 3D pyBullet viewer and check that the robot is not abnormally tilted and that the ball is seen at the
  proper position

## Foot pressure check

- Put the robot on the ground
- Run `tare`, check that the output is OK
- Go to `/lowlevel/left_pressure` and monitor the values `plot pressure_0 pressure_1 pressure_2 pressure_3`, press
  the jauges and check that it is moving positively
- Do the same for right foot in `/lowlevel/right_pressure`

## Global integration test

- The robot should be able to score a goal by walking from the middle of the field to the ball and kick.