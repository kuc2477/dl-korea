import React, { PropTypes } from 'react'
import CardTitle from 'material-ui/Card/CardTitle'
import PlanDashboard from './PlanDashboard'
import PlanForm from './PlanForm'


export default class PlanDetail extends React.Component {
  static propTypes = {
    title: PropTypes.string,
    startAt: PropTypes.string,
    endAt: PropTypes.string,
  };

  static defaultProps = {
    title: 'Plan Title',
    startAt: null,
    endAt: null,
  };

  _generateSubtitle() {
    const { startAt, endAt } = this.props
    return startAt && endAt ? `${startAt} ~ ${endAt}` :
      startAt ? `${startAt} ~` :
      endAt ? `~ ${endAt}` :
      'Period not configured yet'
  }

  render() {
    const { title, startAt, endAt } = this.props
    const subtitle = this._generateSubtitle()

    return (
      <div>
        <CardTitle title={title} subtitle={subtitle} />
        <PlanDashboard />
        <PlanForm />
      </div>
    )
  }
}
