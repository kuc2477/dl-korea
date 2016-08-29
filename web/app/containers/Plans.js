import React from 'react'
import { connect } from 'react-redux'
import Container from './Container'
import PlanList from '../components/plans/PlanList'
import PlanDetail from '../components/plans/PlanDetail'


export class Plans extends React.Component {
  render() {
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
