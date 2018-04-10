# Interactive bar plot visualization with Matplotlib

## Overview
This demo shows the use of the *RectangleSelector* widget to create an interactive bar plot in Matplotlib.

The code is an implementation of the "Range tool" visual representation strategy proposed by Ferreira et al. (2014). This tool is used to "evaluate the probability of a distributions's value falling within a range".

The dataset contains four normal distributions with different means and standard deviations. After initial plotting of the barcharts and their corresponding 95% confidence intervals, the *y* range is set by the user by dragging a horizontal strip, and the computed probability (ranging from 0.0 to 1.0) for each bar is then  mapped as a color.

Plots are automatically updated during interaction.

## Dependencies
matplotlib==2.0.0, numpy==1.14.0

## Credits
Ferreira, N., Fisher, D., & Konig, A. C. (2014, April). Sample-oriented task-driven visualizations: allowing users to make better, more confident decisions. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 571-580). ACM.