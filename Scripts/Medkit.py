from Scripts.base_classes import CollectibleItem


class Medkit(CollectibleItem):
    def __init__(self, x, y, image_path, heal_amount=100):
        super().__init__(x, y, image_path)
        self.heal_amount = heal_amount

    def use(self, player):
        if self.rect.colliderect(player.rect):
            player.get_health(self.heal_amount)
            self.kill()
            return True
        return False