import _ from 'lodash'
import React, { PropTypes } from 'react'
import Immutable from 'immutable'
import ImmutablePropTypes from 'react-immutable-proptypes'
import Subheader from 'material-ui/Subheader'
import ContentAdd from 'material-ui/svg-icons/content/add'
import FloatingActionButton from 'material-ui/FloatingActionButton'
import { CardTitle } from 'material-ui/Card'
import { List } from 'material-ui/List'
import { PlanItem } from './PlanItem'
import { PLAN_CREATION } from '../../constants/routes'
import { PlanPropType } from '../../constants/types'
import { PLANS_CREATION } from '../../constants/strings'


export default class PlanList extends React.Component {
  static contextTypes = {
    router: PropTypes.object.isRequired
  };

  static propTypes = {
    plans: ImmutablePropTypes.listOf(PropTypes.number),
    plansById: ImmutablePropTypes.contains(PlanPropType),
  };

  static defaultProps = {
    plans: Immutable.List(),
    plansById: Immutable.Map(),
  };

  static LIST_STYLE = {};
  static FAB_STYLE = {
    position: 'fixed',
    bottom: 100,
  };

  _getTitle() {
    return 'Plans'
  }

  _getSubtitle() {
    const { plans } = this.props
    return `Total ${plans.size} plans registered`
  }

  routeToCreation() {
    this.context.router.push(PLAN_CREATION.path)
  }

  render() {
    const { LIST_STYLE, FAB_STYLE } = this.constructor
    const { plans, plansById } = this.props

    const planItems = plans.map(id => <PlanItem plan={plansById.get(id)} />)
    const title = this._getTitle()
    const subtitle = this._getSubtitle()

    return (      
      <div>
        <CardTitle title={title} subtitle={subtitle} />

        <List style={LIST_STYLE}>
          {planItems}
        </List>

        <div className="row end-md">
          <FloatingActionButton 
            secondary
            style={FAB_STYLE} 
            onClick={::this.routeToCreation}
          >
            <ContentAdd />
          </FloatingActionButton>
        </div>

      </div>
    )
  }
}
