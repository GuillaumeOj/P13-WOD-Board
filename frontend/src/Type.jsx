import PropTypes from 'prop-types';

export const TokenPropType = PropTypes.shape({
  access_token: PropTypes.string.isRequired,
  token_type: PropTypes.string.isRequired,
});

export const UnitPropType = PropTypes.shape({
  id: PropTypes.number,
  name: PropTypes.string.isRequired,
  symbol: PropTypes.string.isRequired,
});

export const EquipementPropType = PropTypes.shape({
  id: PropTypes.number,
  name: PropTypes.string.isRequired,
  unitId: PropTypes.number,
  unit: UnitPropType,
});

export const MovementPropType = PropTypes.shape({
  id: PropTypes.number,
  name: PropTypes.string.isRequired,
  unitId: PropTypes.number,
  unit: UnitPropType,
  equipments: PropTypes.arrayOf(EquipementPropType),
});

export const GoalPropType = PropTypes.shape({
  id: PropTypes.number,
  movementId: PropTypes.number,
  roundId: PropTypes.number,
  repetition: PropTypes.number.isRequired,
  durationSeconds: PropTypes.number.isRequired,
  movement: MovementPropType.isRequired,
  equipments: PropTypes.arrayOf(EquipementPropType),
});

export const RoundPropType = PropTypes.shape({
  id: PropTypes.number,
  position: PropTypes.number.isRequired,
  repetition: PropTypes.number,
  durationSeconds: PropTypes.number,
  wodId: PropTypes.number.isRequired,
});

export const WodTypePropType = PropTypes.shape({
  id: PropTypes.number,
  name: PropTypes.string.isRequired,
});

export const WodPropType = PropTypes.shape({
  id: PropTypes.number.isRequired,
  title: PropTypes.string.isRequired,
  description: PropTypes.string,
  date: PropTypes.string.isRequired,
  wodTypeId: PropTypes.number,
  authorId: PropTypes.number.isRequired,
  isComplete: PropTypes.bool.isRequired,
});
