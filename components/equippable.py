from components.base_component import BaseComponent
from equipment_types import EquipmentType
import exceptions

class Equippable(BaseComponent):

  def __init__(self, equipment_type,
                     power_bonus=0,
                     defense_bonus=0,
                     accuracy_bonus=0,
                     max_shields=0,
                     max_energy_level=0):
    """Some items require energy to work and require you install an energy cell in them.
    Efficiency is how many charges a single energy cell will provide. By default,
    a energized item will be found will full power."""
    self.equipment_type = equipment_type
    self._power_bonus = power_bonus
    self._defense_bonus = defense_bonus
    self._accuracy_bonus = accuracy_bonus
    self.max_shields = max_shields
    self.current_shields = max_shields
    self.max_energy_level = max_energy_level
    self.current_energy_level = self.max_energy_level

  @property
  def is_energized(self):
    if self.max_energy_level > 0 and self.current_energy_level <= 0:
      return False
    # Items that don't require energy are always "energized"
    return True

  @property
  def power_bonus(self):
    if self.is_energized:
      return self._power_bonus
    else:
      return 0

  @property
  def defense_bonus(self):
    if self.is_energized:
      return self._defense_bonus
    else:
      return 0

  @property
  def accuracy_bonus(self):
    if self.is_energized:
      return self._accuracy_bonus
    else:
      return 0

  def energize(self, energy_cell):
    if self.max_energy_level == 0:
      raise exceptions.Impossible('That item does not require energy.')
    elif self.current_energy_level >= self.max_energy_level:
      raise exceptions.Impossible('That item is already as maximum energy.')

    self.current_energy_level += energy_cell.amount
    if self.current_energy_level > self.max_energy_level:
      self.current_energy_level = self.max_energy_level
    self.current_shields += energy_cell.amount
    if self.current_shields > self.max_shields:
      self.current_shields = self.max_shields

    energy_cell.consume()

  def deplete(self, amount=1):
    over_depletion = 0
    if self.current_energy_level > 0:
      self.current_energy_level -= amount
      if self.current_energy_level < 0:
        overdepletion = abs(self.current_energy_level)
        self.current_energy_level = 0
    return over_depletion

  def after_melee_damage(self, damage_dealt, target=None):
    """ Allows subclasses to provide rider effects after they do melee damage to an actor
    """
    pass

  def after_ranged_damage(self, damage_dealt, target=None):
    """ Allows subclasses to provide rider effects after they do ranged damage to an actor"""
    pass


  def after_damaged(self, damage_taken, source=None):
    """ Allows subclasses to provide rider effects after the equipped entity
    takes damage"""
    pass


class Knife(Equippable):
  def __init__(self):
    super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, power_bonus=2)

class PowerFist(Equippable):
  def __init__(self):
    super().__init__(equipment_type=EquipmentType.MELEE_WEAPON, power_bonus=4,
                     max_energy_level=10)

class Gun(Equippable):
  def __init__(self):
    super().__init__(equipment_type=EquipmentType.RANGED_WEAPON, accuracy_bonus=1,
                    max_energy_level=6)

class SpacersSuit(Equippable):
  def __init__(self):
    super().__init__(equipment_type=EquipmentType.OUTFIT, defense_bonus=1)

class ArmoredSpacersSuit(Equippable):
  def __init__(self):
    super().__init__(equipment_type=EquipmentType.OUTFIT, defense_bonus=3)

class PoweredSpacersSuit(Equippable):
  def __init__(self):
    super().__init__(equipment_type=EquipmentType.OUTFIT, defense_bonus=3,
                    max_shields=20, max_energy_level=20)