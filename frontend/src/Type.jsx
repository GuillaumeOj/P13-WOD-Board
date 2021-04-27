import PropTypes from 'prop-types';

export const TokenPropType = PropTypes.shape({
  access_token: PropTypes.string.isRequired,
  token_type: PropTypes.string.isRequired,
});

export const RoundPropType = PropTypes.shape({
  position: PropTypes.number.isRequired,
  repetition: PropTypes.number.isRequired,
  durationMinutes: PropTypes.number.isRequired,
  durationSeconds: PropTypes.number.isRequired,
});

export const MovementPropType = PropTypes.shape({
  name: PropTypes.string.isRequired,
  repetition: PropTypes.number.isRequired,
  durationMinutes: PropTypes.number.isRequired,
  durationSeconds: PropTypes.number.isRequired,
});
