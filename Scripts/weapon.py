from Scripts.base_classes import CollectibleItem


class Weapon(CollectibleItem):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)

    def use(self, player):
        if self.rect.colliderect(player.rect):
            player.weapon_image = self.image.copy()
            self.kill()
            return True
        return False
