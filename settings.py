import configparser, os, pygame

configParser = configparser.RawConfigParser()
configFilePath = 'gameSettings.cfg'

class Settings():
    def get(self, section, config):
        configParser.read(configFilePath)
        return configParser.get(section, config)

    def set(self, section, config, newConfig):
        configParser[section][config] = newConfig
        with open('gameSettings.cfg', 'w') as configFile:
            configParser.write(configFile)

    def openScreen(self, screen_size, display):
        sttngs_bg = pygame.Rect(50, 50, screen_size[0] - 100, screen_size[1] - 100)
        sttngs_bg = pygame.draw.rect(display, (255,255,255), sttngs_bg, border_radius=20)

        font = pygame.font.Font('freesansbold.ttf', 50)
        title = font.render('Game Settings', True, (0,0,0))
        display.blit(title, (sttngs_bg.width / 2 - title.get_rect().width / 2, 100))

        font = pygame.font.Font('freesansbold.ttf', 30)
        res_label = font.render('Resolution:', True, (0,0,0))
        res_pos = [sttngs_bg.x + 50, sttngs_bg.y + sttngs_bg.height/4]
        display.blit(res_label, res_pos)
        resolutions = ((1024, 576), (1280, 720), (1600, 900), (1920, 1080))
        for res in resolutions:
            res_pos[0] += 300
            res_option = font.render('{} x {}'.format(res[0], res[1]), True, (0,0,0))
            display.blit(res_option, res_pos)

        font = pygame.font.Font('freesansbold.ttf', 30)
        bg_label = font.render('Background:', True, (0,0,0))
        bg_pos = [sttngs_bg.x + 50, sttngs_bg.y + sttngs_bg.height*2/4]
        display.blit(bg_label, bg_pos)
        bgrounds = {
            'MountainsSunset': pygame.image.load('assets/images/MountainsSunset.png'),
            'DarkForest': pygame.image.load('assets/images/DarkForest.png'),
            'DarkSunset': pygame.image.load('assets/images/DarkSunset.png')
            }
        for bg_name, bg_img in bgrounds.items():
            bg_pos[0] += 300
            if bg_name == self.get('screenSettings', 'background'):
                bg_selection_pos = bg_pos
            bg_img = pygame.transform.scale(bg_img, (160,90))
            display.blit(bg_img, bg_pos)

        font = pygame.font.Font('freesansbold.ttf', 30)
        color_label = font.render('Ball Color:', True, (0,0,0))
        color_pos = [sttngs_bg.x + 50, sttngs_bg.y + sttngs_bg.height*3/4]
        display.blit(color_label, color_pos)
        colors = ((200, 100, 50), (209, 10, 10), (80, 5, 161), (29, 103, 222))
        color_pos[0] += 50
        for color in colors:
            radius = 50
            color_pos[0] += 300
            if ','.join(map(str, color)) == self.get('playerSettings', 'ballcolor'):
                color_selection_pos = color_pos
            pygame.draw.circle(display, color, color_pos, radius)

        pygame.display.update()

        backToGame = False
        quit = False
        while not backToGame and not quit:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    save_button = pygame.Rect((sttngs_bg.width/2 - 150, sttngs_bg.y + sttngs_bg.height*7/8), (300, 50))
                    save_button = pygame.draw.rect(display, (200, 100, 50), save_button)
                    font = pygame.font.Font('freesansbold.ttf', 30)
                    save_text = font.render('Save Changes', True, (0,0,0))
                    display.blit(save_text, (save_button.x + save_button.width/2 - save_text.get_width()/2, save_button.y + save_button.height/2 - save_text.get_height()/2))

                    if save_button.x <= mouse[0] <= save_button.x + save_button.width and save_button.y <= mouse[1] <= save_button.y + save_button.height:
                        backToGame = True
                        
                    res_pos[0] -= len(resolutions) * 300
                    for res in resolutions:
                        res_pos[0] += 300
                        res_option_end = [res_pos[0] + res_option.get_width(), res_pos[1] + res_option.get_height()]
                        if res_pos[0] <= mouse[0] <= res_option_end[0] and res_pos[1] <= mouse[1] <= res_option_end[1]:
                            self.set('screenSettings', 'width', str(res[0]))
                            self.set('screenSettings', 'height', str(res[1]))

                    bg_pos[0] -= len(bgrounds) * 300
                    for bg in bgrounds:
                        bg_pos[0] += 300
                        bg_option_end = [bg_pos[0] + 160, bg_pos[1] + 90]
                        if bg_pos[0] <= mouse[0] <= bg_option_end[0] and bg_pos[1] <= mouse[1] <= bg_option_end[1]:
                            self.set('screenSettings', 'background', bg)
                    
                    color_pos[0] -= len(colors) * 300
                    for color in colors:
                        color_pos[0] += 300
                        color_option_end = [color_pos[0] + radius, color_pos[1] + radius]
                        if color_pos[0] - radius <= mouse[0] <= color_option_end[0] and color_pos[1] - radius <= mouse[1] <= color_option_end[1]:
                            str_color = ','.join(map(str, color))
                            self.set('playerSettings', 'ballcolor', str_color)
            pygame.display.update()

        if quit:
            return 'Quit'
