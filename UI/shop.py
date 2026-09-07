import pygame
import pygame.freetype

from .assets import load_font, load_image, load_sound

pygame.init()
pygame.font.init()


class power_ups:
    """shoppable item"""

    def __init__(
        self,
        item_no: int,
        name: str,
        price: int,
        icon: pygame.Surface,
        frame_rect: pygame.Rect,
        icon_topleft: tuple[int, int],
        price_text_pos: tuple[int, int],
        name_text_pos: tuple[int, int],
    ):
        self.item_no = item_no
        self.name = name
        self.price = price
        self.icon = icon
        self.frame_rect = frame_rect
        self.icon_topleft = icon_topleft
        self.price_text_pos = price_text_pos
        self.name_text_pos = name_text_pos

    def try_purchase(self, shop: "Shop") -> None:
        if shop.coin >= self.price:
            shop.buy_sound.play()
            shop._show_text(f"Item {self.name} purchased!")
            shop.coin -= self.price
            shop.purchased_item_no = self.item_no
        else:
            shop._show_text("Not enough coins!")


class SkipPowerUp(power_ups):
    def __init__(self, icon: pygame.Surface, frame_rect: pygame.Rect):
        super().__init__(
            item_no=1,
            name="Skips",
            price=500,
            icon=icon,
            frame_rect=frame_rect,
            icon_topleft=(240, 340),
            price_text_pos=(390, 370),
            name_text_pos=(370, 330),
        )


class FiftyFiftyPowerUp(power_ups):
    def __init__(self, icon: pygame.Surface, frame_rect: pygame.Rect):
        super().__init__(
            item_no=2,
            name="Fifty-fifty",
            price=500,
            icon=icon,
            frame_rect=frame_rect,
            icon_topleft=(690, 340),
            price_text_pos=(840, 370),
            name_text_pos=(790, 330),
        )


class DoubleAwardPowerUp(power_ups):
    def __init__(self, icon: pygame.Surface, frame_rect: pygame.Rect):
        super().__init__(
            item_no=3,
            name="Double award",
            price=500,
            icon=icon,
            frame_rect=frame_rect,
            icon_topleft=(240, 540),
            price_text_pos=(390, 570),
            name_text_pos=(330, 530),
        )


class ShieldPowerUp(power_ups):
    def __init__(self, icon: pygame.Surface, frame_rect: pygame.Rect):
        super().__init__(
            item_no=4,
            name="Shield",
            price=500,
            icon=icon,
            frame_rect=frame_rect,
            icon_topleft=(690, 543),
            price_text_pos=(840, 570),
            name_text_pos=(820, 530),
        )


class Shop:
    """Shop screen"""

    def __init__(self, screen):
        self.screen = screen

        self.buy_sound = load_sound("Sound Effect", "buy_item.mp3")
        self.button_sound = load_sound("Sound Effect", "button.mp3")

        self.frame = load_image("Game Assets", "frame_player.png", size=(360, 160), label="")
        self.frame_pressed = load_image("Game Assets", "frame_player_pressed.png", size=(360, 160), label="")
        self.frame_rect1 = self.frame.get_rect(topleft=(200, 300))
        self.frame_rect2 = self.frame.get_rect(topleft=(650, 300))
        self.frame_rect3 = self.frame.get_rect(topleft=(200, 500))
        self.frame_rect4 = self.frame.get_rect(topleft=(650, 500))
        self.shop_title = load_image("Game Assets", "SHOP_title.png", size=(400, 80), label="SHOP")

        self.quit_button = load_image("Game Assets", "quit_button.png", size=(48, 48), label="X")
        self.quit_button_rect = self.quit_button.get_rect(topright=(1190, 10))

        self.frame_return = load_image("Game Assets", "button.png", size=(220, 70), label="")
        self.frame_return_pressed = load_image("Game Assets", "button_pressed.png", size=(220, 70), label="")
        self.frame_return_rect = self.frame_return.get_rect(center=(600, 700))

        self.return_text = load_image("Game Assets", "RETURN.png", size=(180, 50), label="RETURN")
        self.return_pressed = load_image("Game Assets", "RETURN_pressed.png", size=(180, 50), label="RETURN")
        self.return_rect = self.return_text.get_rect(center=(600, 700))

        self.items = load_image("Game Assets", "ITEMS.png", size=(160, 48), label="ITEMS")
        self.items_pressed = load_image("Game Assets", "ITEMS_pressed.png", size=(160, 48), label="ITEMS")
        self.items_rect = self.items.get_rect(center=(1050, 50))

        self.shop = load_image("Game Assets", "SHOP.png", size=(160, 48), label="SHOP")
        self.shop_pressed = load_image("Game Assets", "SHOP_pressed.png", size=(160, 48), label="SHOP")
        self.shop_rect = self.shop.get_rect(center=(875, 50))

        self.top_button = load_image("Game Assets", "top_button.png", size=(180, 56), label="")
        self.top_button_pressed = load_image("Game Assets", "top_button_pressed.png", size=(180, 56), label="")
        self.top_button_items_rect = self.top_button.get_rect(center=(1050, 50))
        self.top_button_shop_rect = self.top_button.get_rect(center=(875, 50))

        self.icon1 = load_image("Game Assets", "shop_icon1.png", size=(80, 80), label="1")
        self.icon2 = load_image("Game Assets", "shop_icon2.png", size=(80, 80), label="2")
        self.icon3 = load_image("Game Assets", "shop_icon3.png", size=(80, 80), label="3")
        self.icon4 = load_image("Game Assets", "shop_icon4.png", size=(80, 80), label="4")

        self.font = load_font(30)

        self.power_slots: tuple[power_ups, ...] = (
            SkipPowerUp(self.icon1, self.frame_rect1),
            FiftyFiftyPowerUp(self.icon2, self.frame_rect2),
            DoubleAwardPowerUp(self.icon3, self.frame_rect3),
            ShieldPowerUp(self.icon4, self.frame_rect4),
        )
        self._sync_legacy_power_attrs()

        self.coin = 2000
        self.text = ""
        self.text_shown_at_ms = 0
        self.text_duration_ms = 3000
        self.purchased_item_no = 0

    def _sync_legacy_power_attrs(self) -> None:
        """keep icon number, name, and rects in sync with power slots"""
        for i, slot in enumerate(self.power_slots, start=1):
            setattr(self, f"icon{i}", slot.icon)
            setattr(self, f"icon{i}_no", slot.price)
            setattr(self, f"icon{i}_name", slot.name)
            setattr(self, f"frame_rect{i}", slot.frame_rect)

    def _show_text(self, msg: str):
        self.text = msg
        self.text_shown_at_ms = pygame.time.get_ticks()

    def pop_purchased_item(self) -> int:
        """Return last purchased item id"""
        item_no = self.purchased_item_no
        self.purchased_item_no = 0
        return item_no

    def update(self, events):
        """Handle clicks and hover."""
        mouse_pos = pygame.mouse.get_pos()

        if self.frame_return_rect.collidepoint(mouse_pos):
            self.current_button = self.frame_return_pressed
            self.current_return = self.return_pressed
        else:
            self.current_button = self.frame_return
            self.current_return = self.return_text

        if self.top_button_items_rect.collidepoint(mouse_pos):
            self.current_top_button_items = self.top_button_pressed
            self.current_items = self.items_pressed
        else:
            self.current_top_button_items = self.top_button
            self.current_items = self.items

        self.current_frame1 = (
            self.frame_pressed if self.power_slots[0].frame_rect.collidepoint(mouse_pos) else self.frame
        )
        self.current_frame2 = (
            self.frame_pressed if self.power_slots[1].frame_rect.collidepoint(mouse_pos) else self.frame
        )
        self.current_frame3 = (
            self.frame_pressed if self.power_slots[2].frame_rect.collidepoint(mouse_pos) else self.frame
        )
        self.current_frame4 = (
            self.frame_pressed if self.power_slots[3].frame_rect.collidepoint(mouse_pos) else self.frame
        )

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.frame_return_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 6
                if self.top_button_items_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 11
                if self.quit_button_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    return 2
                for slot in self.power_slots:
                    if slot.frame_rect.collidepoint(event.pos):
                        slot.try_purchase(self)
                        break

        return 10

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.quit_button, self.quit_button_rect)
        self.screen.blit(self.current_top_button_items, self.top_button_items_rect)
        self.screen.blit(self.top_button_pressed, self.top_button_shop_rect)
        self.screen.blit(self.current_items, self.items_rect)
        self.screen.blit(self.shop_pressed, self.shop_rect)
        self.screen.blit(self.current_button, self.frame_return_rect)
        self.screen.blit(self.current_return, self.return_rect)

        self.screen.blit(self.shop_title, (400, 100))

        self.screen.blit(self.current_frame1, self.frame_rect1)
        self.screen.blit(self.current_frame2, self.frame_rect2)
        self.screen.blit(self.current_frame3, self.frame_rect3)
        self.screen.blit(self.current_frame4, self.frame_rect4)

        for slot in self.power_slots:
            self.screen.blit(slot.icon, slot.icon_topleft)
            self.font.render_to(
                self.screen, slot.price_text_pos, str(slot.price), (255, 255, 255)
            )
            self.font.render_to(self.screen, slot.name_text_pos, str(slot.name), (255, 255, 255))

        self.font.render_to(self.screen, (100, 100), "Coins: " + str(self.coin), (255, 255, 255))

        if self.text and pygame.time.get_ticks() - self.text_shown_at_ms <= self.text_duration_ms:
            self.text_surf, self.text_rect = self.font.render(self.text, (255, 255, 255))
            self.text_rect.center = (600, 750)
            self.screen.blit(self.text_surf, self.text_rect)


if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 800))
    window = Shop(screen)
    clock = pygame.time.Clock()
    num = 10
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if num == 10:
            num = window.update(events)
            window.draw()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
