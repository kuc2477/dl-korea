import Immutable from 'immutable'
import { PropTypes } from 'react'
import ImmutablePropTypes from 'react-immutable-proptypes'


// ==================
// Extended proptypes
// ==================

export const ValueLinkPropType = PropTypes.shape({
  value: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number,
    PropTypes.object,
    PropTypes.array,
    PropTypes.bool,
  ]),
  requestChange: PropTypes.func
})


// ================
// Scheme proptypes
// ================

export const UserPropType = ImmutablePropTypes.contains({
  id: PropTypes.number,
  firstname: PropTypes.string,
  lastname: PropTypes.string,
})

