import _ from 'lodash'
import React, { PropTypes } from 'react'
import SwipeableViews from 'react-swipeable-views'
import { connect } from 'react-redux'
import Container from './Container'
import PlanDetail from '../components/plans/PlanDetail'
import PlanList from '../components/plans/PlanList'


export class Plans extends React.Component {
  static SWIPEABLE_CONTAINER_STYLE = {
    height: '100%',
  };

  render() {
    const { SWIPEABLE_CONTAINER_STYLE } = this.constructor

    return (
      <Container>
        <div className="col-md-offset-2 col-md-5">
          <PlanDetail />
        </div>
        <div className="col-md-offset-1 col-md-3">
          <PlanList />
        </div>
      </Container>
    )
  }
}


export default connect(plans => ({
}))(Plans)
