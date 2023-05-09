## Asabidi (9.5/15P)

### 1 Karaoke Game (3/6P)

 * frequency detection
   * kind of detects correct frequencies sometimes (+1.5)
   * I had to add filtering (for both amplitude and frequency) to get rid of background noise. It wouldn't have worked otherwise. (-1.5)
 * game
   * seems to work? pretty hard to test with the malfunctioning frequency detection. Also, the sample sounds for C4 and B4 sound exactly the same to me. (+1.5)
 * latency
   * latency is high and gets even higher as the program runs (-1)

### 2 Whistle Input (6/8P)

 * whiste detection
   * works (+3)
 * robust against noise
   * was able to trigger events by clapping and hissing (-1)
   * did not trigger from ordinary background noise (+1)
 * latency
   * latency is high and gets even higher as the program runs (-1)
 * pyglet test program
   * seems to work (+1)
 * triggered key events
   * seems to work (+1)

## Bonus Point: (0.5/1P)

Lots of magic numbers (-0.5), otherwise ok (+0.5).
