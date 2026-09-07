import pygame
import pygame.freetype

from .assets import load_font, load_image, load_sound

pygame.init()
pygame.font.init()


class bag_power_ups:

    def __init__(self, item_no: int, frame_rect: pygame.Rect, equip_pos_label: tuple[int, int]):
        self.item_no = item_no
        self.frame_rect = frame_rect
        self.equip_pos_label = equip_pos_label

    def count(self, bag: "Shop") -> int:
        return int(getattr(bag, f"icon{self.item_no}_no"))

    def try_toggle_equip(self, bag: "Shop") -> None:
        bag.button_sound.play()
        if bag.equip_pos == self.equip_pos_label:
            bag.current_equip, bag.equip_rect = bag.font.render("", (255, 255, 255))
            bag.equip_pos = (0, 0)
        else:
            bag.current_equip = bag.equip
            bag.equip_pos = self.equip_pos_label


class SkipBagSlot(bag_power_ups):
    def __init__(self, frame_rect: pygame.Rect):
        super().__init__(1, frame_rect, (400, 420))


class FiftyFiftyBagSlot(bag_power_ups):
    def __init__(self, frame_rect: pygame.Rect):
        super().__init__(2, frame_rect, (850, 420))


class DoubleAwardBagSlot(bag_power_ups):
    def __init__(self, frame_rect: pygame.Rect):
        super().__init__(3, frame_rect, (400, 620))


class ShieldBagSlot(bag_power_ups):
    def __init__(self, frame_rect: pygame.Rect):
        super().__init__(4, frame_rect, (850, 620))


class Shop:
    """equip consumable items"""

    def __init__(self, screen):
        self.screen = screen

        self.button_sound = load_sound("Sound Effect", "button.mp3")

        self.frame = load_image("Game Assets", "frame_player.png", size=(360, 160), label="")
        self.frame_pressed = load_image("Game Assets", "frame_player_pressed.png", size=(360, 160), label="")
        self.frame_grey = load_image("Game Assets", "frame_player_grey.png", size=(360, 160), label="")
        self.frame_rect1 = self.frame.get_rect(topleft = (200, 300))
        self.frame_rect2 = self.frame.get_rect(topleft = (650, 300))
        self.frame_rect3 = self.frame.get_rect(topleft = (200, 500))
        self.frame_rect4 = self.frame.get_rect(topleft = (650, 500))
        self.items_title = load_image("Game Assets", "ITEMS_title.png", size=(400, 80), label="ITEMS")

        self.quit_button = load_image("Game Assets", "quit_button.png", size=(48, 48), label="X")
        self.quit_button_rect = self.quit_button.get_rect(topright = (1190, 10))

        self.frame_return = load_image("Game Assets", "button.png", size=(220, 70), label="")
        self.frame_return_pressed = load_image("Game Assets", "button_pressed.png", size=(220, 70), label="")
        self.frame_return_rect = self.frame_return.get_rect(center = (600, 700))

        self.return_text = load_image("Game Assets", "RETURN.png", size=(180, 50), label="RETURN")
        self.return_pressed = load_image("Game Assets", "RETURN_pressed.png", size=(180, 50), label="RETURN")
        self.return_rect = self.return_text.get_rect(center = (600, 700))

        self.items = load_image("Game Assets", "ITEMS.png", size=(160, 48), label="ITEMS")
        self.items_pressed = load_image("Game Assets", "ITEMS_pressed.png", size=(160, 48), label="ITEMS")
        self.items_rect = self.items.get_rect(center = (1050, 50))

        self.shop = load_image("Game Assets", "SHOP.png", size=(160, 48), label="SHOP")
        self.shop_pressed = load_image("Game Assets", "SHOP_pressed.png", size=(160, 48), label="SHOP")
        self.shop_rect = self.shop.get_rect(center = (875, 50))

        self.top_button = load_image("Game Assets", "top_button.png", size=(180, 56), label="")
        self.top_button_pressed = load_image("Game Assets", "top_button_pressed.png", size=(180, 56), label="")
        self.top_button_items_rect = self.top_button.get_rect(center = (1050, 50))
        self.top_button_shop_rect = self.top_button.get_rect(center = (875, 50))

        self.icon1 = load_image("Game Assets", "shop_icon1.png", size=(80, 80), label="1")
        self.icon2 = load_image("Game Assets", "shop_icon2.png", size=(80, 80), label="2")
        self.icon3 = load_image("Game Assets", "shop_icon3.png", size=(80, 80), label="3")
        self.icon4 = load_image("Game Assets", "shop_icon4.png", size=(80, 80), label="4")

        self.font = load_font(30)
        
        self.icon1_name = "Skips"
        self.icon2_name = "Fifty-fifty"
        self.icon3_name = "Double award"
        self.icon4_name = "Shield"

        self.icon1_no = 0
        self.icon2_no = 0
        self.icon3_no = 0
        self.icon4_no = 0

        self.equip, self.equip_rect = self.font.render("Equipped!", (255, 255, 255))
        self.current_equip, self.equip_rect = self.font.render("", (255, 255, 255))
        self.equip_pos = (0, 0)
        self.skip_consume_on_return = False

        self.bag_slots: tuple[bag_power_ups, ...] = (
            SkipBagSlot(self.frame_rect1),
            FiftyFiftyBagSlot(self.frame_rect2),
            DoubleAwardBagSlot(self.frame_rect3),
            ShieldBagSlot(self.frame_rect4),
        )

    def has_equipped_item(self) -> bool:
        return self.equip_pos != (0, 0)

    def get_equipped_item_no(self) -> int:
        return self._equipped_item_no()

    def invalidate_equipped_item_no_consume(self):
        self.skip_consume_on_return = True
        self.current_equip, self.equip_rect = self.font.render("", (255, 255, 255))
        self.equip_pos = (0, 0)

    def consume_equipped_item(self):
        equipped_item_no = self._equipped_item_no()
        if equipped_item_no == 1:
            self.icon1_no = max(0, self.icon1_no - 1)
        elif equipped_item_no == 2:
            self.icon2_no = max(0, self.icon2_no - 1)
        elif equipped_item_no == 3:
            self.icon3_no = max(0, self.icon3_no - 1)
        elif equipped_item_no == 4:
            self.icon4_no = max(0, self.icon4_no - 1)
        self.current_equip, self.equip_rect = self.font.render("", (255, 255, 255))
        self.equip_pos = (0, 0)

    def _equipped_item_no(self) -> int:
        if self.equip_pos == (400, 420):
            return 1
        if self.equip_pos == (850, 420):
            return 2
        if self.equip_pos == (400, 620):
            return 3
        if self.equip_pos == (850, 620):
            return 4
        return 0

    def update_contents(self, item_no):
        if item_no == 1:
            self.icon1_no += 1
        elif item_no == 2:
            self.icon2_no += 1
        elif item_no == 3:
            self.icon3_no += 1
        elif item_no == 4:
            self.icon4_no += 1
        
    def update(self, events):
        """Handle clicks and hover."""
        mouse_pos = pygame.mouse.get_pos()

        if self.frame_return_rect.collidepoint(mouse_pos):
            self.current_button = self.frame_return_pressed
            self.current_return = self.return_pressed
        else:
            self.current_button = self.frame_return
            self.current_return = self.return_text

        if self.top_button_shop_rect.collidepoint(mouse_pos):
            self.current_top_button_shop = self.top_button_pressed
            self.current_shop = self.shop_pressed
        else:
            self.current_top_button_shop = self.top_button
            self.current_shop = self.shop

        frames: list[pygame.Surface] = []
        for slot in self.bag_slots:
            if slot.count(self) == 0:
                frames.append(self.frame_grey)
            elif slot.frame_rect.collidepoint(mouse_pos):
                frames.append(self.frame_pressed)
            else:
                frames.append(self.frame)
        self.current_frame1, self.current_frame2, self.current_frame3, self.current_frame4 = frames

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.frame_return_rect.collidepoint(event.pos):
                    # Returning from items screen should not auto-consume equipped items.
                    # Items are consumed and applied when the question starts unless the question is daily double.
                    self.button_sound.play()
                    self.skip_consume_on_return = False
                    return 6
                if self.top_button_shop_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 10
                if self.quit_button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2
                for slot in self.bag_slots:
                    if slot.frame_rect.collidepoint(event.pos) and slot.count(self) > 0:
                        slot.try_toggle_equip(self)
                        break
        
        return 11

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.quit_button, self.quit_button_rect)
        self.screen.blit(self.top_button_pressed, self.top_button_items_rect)
        self.screen.blit(self.current_top_button_shop, self.top_button_shop_rect)
        self.screen.blit(self.items_pressed, self.items_rect)
        self.screen.blit(self.current_shop, self.shop_rect)
        self.screen.blit(self.current_button, self.frame_return_rect)
        self.screen.blit(self.current_return, self.return_rect)

        self.screen.blit(self.items_title, (370, 100))

        self.screen.blit(self.current_frame1, self.frame_rect1)
        self.screen.blit(self.current_frame2, self.frame_rect2)
        self.screen.blit(self.current_frame3, self.frame_rect3)
        self.screen.blit(self.current_frame4, self.frame_rect4)

        self.screen.blit(self.icon1, (240, 340))
        self.screen.blit(self.icon2, (690, 340))
        self.screen.blit(self.icon3, (240, 540))
        self.screen.blit(self.icon4, (690, 543))

        self.font.render_to(self.screen, (400, 370), str(self.icon1_no), (255, 255, 255))
        self.font.render_to(self.screen, (850, 370), str(self.icon2_no), (255, 255, 255))
        self.font.render_to(self.screen, (400, 570), str(self.icon3_no), (255, 255, 255))
        self.font.render_to(self.screen, (850, 570), str(self.icon4_no), (255, 255, 255))

        self.font.render_to(self.screen, (370, 330), str(self.icon1_name), (255, 255, 255))
        self.font.render_to(self.screen, (790, 330), str(self.icon2_name), (255, 255, 255))
        self.font.render_to(self.screen, (330, 530), str(self.icon3_name), (255, 255, 255))
        self.font.render_to(self.screen, (820, 530), str(self.icon4_name), (255, 255, 255))

        equipped_item_no = self._equipped_item_no()
        if (
            (equipped_item_no == 1 and self.icon1_no > 0)
            or (equipped_item_no == 2 and self.icon2_no > 0)
            or (equipped_item_no == 3 and self.icon3_no > 0)
            or (equipped_item_no == 4 and self.icon4_no > 0)
        ):
            self.screen.blit(self.current_equip, self.equip_pos)

if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    window = Shop(screen)
    clock = pygame.time.Clock()
    num = 11
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        if num == 11:
            num = window.update(events)
            window.draw()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()