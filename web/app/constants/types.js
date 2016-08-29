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

export const PlanPropType = ImmutablePropTypes.contains({
  id: PropTypes.number,
  category: PropTypes.string,
  loadUnit: PropTypes.string,
  private: PropTypes.bool,
  active: PropTypes.bool,
  user: PropTypes.number,
  title: PropTypes.string,
  description: PropTypes.string,
  loadIndex: PropTypes.number,
  totalLoad: PropTypes.number,
  dailyLoad: PropTypes.number,
  cron: PropTypes.string,
  startAt: PropTypes.string,
  endAt: PropTypes.string,
})
