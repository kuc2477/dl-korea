import React, { PropTypes } from 'react'
import { ListItem } from 'material-ui/List'
import { PlanPropType } from '../../constants/types'


export default class PlanItem extends React.Component {
  static propTypes = {
    plan: PlanPropType
  };

  render() {
    const { plan } = this.props
    const { title, description, startAt, endAt } = plan.toJS()
    return (
      <ListItem primaryText={title} />
    )
  }
}
