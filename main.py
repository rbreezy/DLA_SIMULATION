#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from matplotlib import pyplot as plt
import os
from dla_helper_file import diffusion_limited_aggregation

def run_simulation():
    dla = diffusion_limited_aggregation(number_of_particles=45000, stickiness_factor=0.9)
    dla.simulate(GIF=True)

if __name__ == '__main__':
    run_simulation()


# In[ ]:




