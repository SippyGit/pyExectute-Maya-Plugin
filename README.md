# pyExectute-Maya-Plugin
Demo Code for the pyExectute Maya Plugin

When writing code for the plugin it is very important to use "output" to store your final output and any or all of the given variables: a, b, c, d.

Example code:

  Import math​

  output = 0​

  if a < 0 or a > 12:​

   output = 0​

  else:​

   normalized = a / 12​

   output = math.sin(math.pi*normalized) * b

NB | When working on plugins make sure you save before testing otherwise the plugin will not update.
