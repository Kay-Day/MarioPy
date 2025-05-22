__author__ = 'marble_xu'

import pygame as pg
from .. import tools
from .. import setup
from .. import constants as c
from ..components import info


class Menu(tools.State):
    def __init__(self):
        tools.State.__init__(self)
        persist = {c.COIN_TOTAL: 0,
                   c.SCORE: 0,
                   c.LIVES: 3,
                   c.TOP_SCORE: 0,
                   c.CURRENT_TIME: 0.0,
                   c.LEVEL_NUM: 1,
                   c.PLAYER_NAME: c.PLAYER_MARIO}
        self.startup(0.0, persist)

    def startup(self, current_time, persist):
        self.next = c.LEVEL  # Chuyển thẳng sang level thay vì LOAD_SCREEN
        self.persist = persist
        self.game_info = persist
        self.overhead_info = info.Info(self.game_info, c.MAIN_MENU)

        self.setup_background()
        self.auto_start_timer = 0  # Timer để tự động bắt đầu game

    def setup_background(self):
        self.background = setup.GFX['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pg.transform.scale(self.background,
                                             (int(self.background_rect.width * c.BACKGROUND_MULTIPLER),
                                              int(self.background_rect.height * c.BACKGROUND_MULTIPLER)))

        self.viewport = setup.SCREEN.get_rect(bottom=setup.SCREEN_RECT.bottom)
        self.image_dict = {}
        image = tools.get_image(setup.GFX['title_screen'], 1, 60, 176, 88,
                                (255, 0, 220), c.SIZE_MULTIPLIER)
        rect = image.get_rect()
        rect.x, rect.y = (170, 100)
        self.image_dict['GAME_NAME_BOX'] = (image, rect)

    def update(self, surface, keys, current_time):
        self.current_time = current_time
        self.game_info[c.CURRENT_TIME] = self.current_time

        # Tự động bắt đầu game sau 2 giây hoặc khi nhấn Enter
        if self.auto_start_timer == 0:
            self.auto_start_timer = current_time
        elif (current_time - self.auto_start_timer) > 2000 or keys[pg.K_RETURN]:
            self.reset_game_info()
            self.done = True

        self.overhead_info.update(self.game_info)

        surface.blit(self.background, self.viewport, self.viewport)
        surface.blit(self.image_dict['GAME_NAME_BOX'][0],
                     self.image_dict['GAME_NAME_BOX'][1])
        self.overhead_info.draw(surface)

    def reset_game_info(self):
        self.game_info[c.COIN_TOTAL] = 0
        self.game_info[c.SCORE] = 0
        self.game_info[c.LIVES] = 3
        self.game_info[c.CURRENT_TIME] = 0.0
        self.game_info[c.LEVEL_NUM] = 1

        self.persist = self.game_info