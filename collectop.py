import pygame
import random


class Collectop:

    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("Calibri", 24)
        self.title_font = pygame.font.SysFont("Calibri", 35)
        
        self.load_images()
        self.new_game()
        self.total_points = 0
        self.points = 0
        self.level = 0
        self.total_time = 0
        self.clock = pygame.time.Clock()
        self.basetime = 2
        self.time_left = self.basetime
        self.timer = pygame.USEREVENT + 1                                                
        pygame.time.set_timer(self.timer, 1000) 
        
        self.height = len(self.stage)
        self.width = len(self.stage[0])
        self.scale = self.images[0].get_width()
        
        window_height = self.height * self.scale
        window_width = self.width * self.scale
        self.window = pygame.display.set_mode((window_width, window_height+30))
        
        pygame.display.set_caption("Collectop")
        
        self.welcome = self.title_font.render(f"Collectop! Press any key to start", True, (255, 255, 255))
        self.window.blit(self.welcome, (10*self.scale-self.welcome.get_width()/2, 3*self.scale))
        pygame.display.flip()
        
        key_down = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    key_down = True
            if key_down == True:
                break
                
        self.main_loop()
        
        
    def load_images(self):
        self.images = []
        for image_name in ["wall", "floor", "robot", "target"]:
            self.images.append(pygame.image.load(image_name + ".png"))
            
            
    def new_game(self):
        self.stage = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        
        self.stage = self.randomize_stage(self.stage)
        
        
    def randomize_stage(self, stage):
        # this method is for randomizing the robot's and the coins' positions after each level
        new_stage = []
        new_stage.append(stage[0])
        for row in stage[1:6]:
            while True:
                index = random.choice(range(20))
                if row[index] == 1:
                    row[index] = 3
                    break
            new_stage.append(row)
        new_stage.append(stage[0])
            
        robot_randrow = random.choice(range(1,6))
        while True:
            index = random.choice(range(20))
            if new_stage[robot_randrow][index] == 1:
                new_stage[robot_randrow][index] = 2
                break

        return new_stage
        
        
    def main_loop(self):
        while True:
            self.check_events()
            self.reload_window()
                
    
    def reload_window(self):
        self.window.fill((0, 0, 0))
        
        for y in range(self.height):
            for x in range(self.width):
                block = self.stage[y][x]
                self.window.blit(self.images[block], (x * self.scale, y * self.scale))
           
        point = self.font.render(f"Points: {self.total_points+self.points}", True, (255, 255, 255))
        lvl = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        t = self.font.render("00:%02d" % self.time_left, True, (255, 255, 255))
        
        self.window.blit(point, (18*self.scale, 7*self.scale+5))
        self.window.blit(lvl, (10, 7*self.scale+5))
        self.window.blit(t, (9*self.scale, 7*self.scale+5))
        
        if self.points == 5:
            self.new_game()
            self.total_points += self.points
            self.level += 1
            self.points = 0
            self.time_left = self.basetime - self.level
            
        pygame.display.flip()
        
           
    def check_events(self):
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                quit()
                
            if event.type == self.timer:
                if self.time_left > 0:
                    self.time_left -= 1
                    self.total_time += 1
                else:
                    self.gameover()
      
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(0, -1)
                if event.key == pygame.K_RIGHT:
                    self.move(0, 1)
                if event.key == pygame.K_UP:
                    self.move(-1, 0)
                if event.key == pygame.K_DOWN:
                    self.move(1, 0)
               
                
    def find_robot(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.stage[y][x] == 2:
                    return (y, x)
                    
                  
    def move(self, move_y, move_x):
        robot_old_y, robot_old_x = self.find_robot() 
        robot_new_y = robot_old_y + move_y
        robot_new_x = robot_old_x + move_x
        
        if robot_new_y in range(self.height) and robot_new_x in range(self.width):
        
            if self.stage[robot_new_y][robot_new_x] in [0, 3]:
                if self.stage[robot_new_y][robot_new_x] == 0:
                    return
                else:
                    self.stage[robot_old_y][robot_old_x] -= 1
                    self.stage[robot_new_y][robot_new_x] -= 1
                    self.points += 1
                    return

            self.stage[robot_old_y][robot_old_x] -= 1
            self.stage[robot_new_y][robot_new_x] += 1
            
            
    def gameover(self):
        self.window.fill((0, 0, 0))
        verdicts = self.font.render(f"Total points: {self.total_points+self.points}  Level reached: {self.level}", True, (255, 255, 255))
        total_t = self.font.render(f"Total time survived: {self.total_time} seconds", True, (255, 255, 255))
        try_again = self.font.render(f"Play again? Y    Quit? Esc", True, (255, 255, 255))
        
        self.window.blit(verdicts, (10*self.scale-verdicts.get_width()/2, 3*self.scale))
        self.window.blit(total_t, (10*self.scale-total_t.get_width()/2, 3.5*self.scale))
        self.window.blit(try_again, (10*self.scale-try_again.get_width()/2, 4*self.scale))
        
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                    if event.key == pygame.K_y:
                        self.play_again()
        
        
    def play_again(self):
        self.new_game()
        self.total_points = 0
        self.points = 0
        self.level = 0
        self.total_time = 0
        self.time_left = self.basetime
        self.main_loop()


if __name__ == "__main__":
    Collectop()
