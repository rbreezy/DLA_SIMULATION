#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import random
import time
import os

matplotlib.use("Agg")

class diffusion_limited_aggregation:
    def __init__(self, number_of_particles, stickiness_factor, N = 400) -> None:
        # initilizing the varibale to use in the simulation
        self.number_of_particles = number_of_particles
        self.N = N
        self.stickiness_factor = stickiness_factor

    def simulate(self, GIF=False):
        start_time = time.time()

        if GIF:
            import imageio

        # making the directory if not available
        if GIF and not os.path.isdir("frames"):
            os.mkdir("frames")
        if GIF and not os.path.isdir("media"):
            os.mkdir("media")


        self.M = int(self.N * 0.8)
        self.grid = np.zeros((self.N, self.N))

        start_rect_x_start = start_rect_y_start = (self.N-self.M) // 2
        start_rect_x_end = start_rect_y_end = (self.N-self.M)//2 + self.M - 1

        seed_x = seed_y = self.N // 2
        self.grid[seed_y, seed_x] = 1
        self.final_length = [0, 1]
        final_x_start = final_x_end = seed_x

        particles_added = 1

        self.growth_time = [0, round(time.time()-start_time, 3)]

        if GIF:
            plt.imshow(self.grid, cmap='Blues', interpolation='none')
            plt.savefig("frames/frame1.png", dpi=300)
            plt.close()

        while particles_added < self.number_of_particles:
            mover_x = random.randint(start_rect_x_start, start_rect_x_end)
            mover_y = random.randint(start_rect_y_start, start_rect_y_end)
            speed = 1

            found_neighbor = False
            grid_touch = False

            while not found_neighbor and not grid_touch:
                if mover_x == 0 or mover_x == self.N-1 or mover_y == 0 or mover_y == self.N-1:
                    grid_touch = True

                if not grid_touch:
                    # Left 
                    if self.grid[mover_y, mover_x-1] == 1:
                        if speed - self.stickiness_factor > 0.1:
                            speed = speed - self.stickiness_factor
                        else:
                            found_neighbor = True
                            self.grid[mover_y, mover_x] = 1
                            particles_added += 1
                            self.growth_time.append(round(time.time()-start_time, 3))
                            if mover_x > final_x_end:
                                final_x_end = mover_x
                            self.final_length.append(final_x_end-final_x_start+1)

                    # Right 
                    elif self.grid[mover_y, mover_x+1] == 1:
                        if speed - self.stickiness_factor > 0.1:
                            speed = speed - self.stickiness_factor
                        else:
                            found_neighbor = True
                            self.grid[mover_y, mover_x] = 1
                            particles_added += 1
                            self.growth_time.append(round(time.time()-start_time, 3))
                            if mover_x < final_x_start:
                                final_x_start = mover_x
                            self.final_length.append(final_x_end-final_x_start+1)
                    
                    # Top
                    elif self.grid[mover_y-1, mover_x] == 1:
                        if speed - self.stickiness_factor > 0.1:
                            speed = speed - self.stickiness_factor
                        else:
                            found_neighbor = True
                            self.grid[mover_y, mover_x] = 1
                            particles_added += 1
                            self.growth_time.append(round(time.time()-start_time, 3))
                            self.final_length.append(final_x_end-final_x_start+1)

                    # Bottom
                    elif self.grid[mover_y+1, mover_x] == 1:
                        if speed - self.stickiness_factor > 0.1:
                            speed = speed - self.stickiness_factor
                        else:                
                            found_neighbor = True
                            self.grid[mover_y, mover_x] = 1
                            particles_added += 1
                            self.growth_time.append(round(time.time()-start_time, 3))
                            self.final_length.append(final_x_end-final_x_start+1)

                # moving the particle to next place
                if not found_neighbor and not grid_touch:
                    rand = random.randint(1, 4)
                    if rand == 1:
                        mover_x -= 1
                    if rand == 2:
                        mover_x += 1
                    if rand == 3:
                        mover_y -= 1
                    if rand == 4:
                        mover_y += 1

            if GIF and found_neighbor:
                if particles_added % 20 == 0:
                    plt.imshow(self.grid, cmap='Blues', interpolation='none')
                    plt.savefig(f"frames/frame{particles_added}.png", dpi=300)
                    plt.close()

        if GIF:
            with imageio.get_writer("media/DLA.gif", mode="I") as writer:
                for i in range(1, particles_added+1):
                    try:
                        frame = imageio.imread(f"frames/frame{i}.png")
                        writer.append_data(frame)
                    except:
                        continue

        end_time = time.time()

        if GIF:
            self.growth_time = None

