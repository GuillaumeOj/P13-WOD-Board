import PropTypes from 'prop-types';

// eslint-disable-next-line import/prefer-default-export
export const TokenPropType = PropTypes.shape({
  access_token: PropTypes.string.isRequired,
  token_type: PropTypes.string.isRequired,
});
