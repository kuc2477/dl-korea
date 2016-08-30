import React, { PropTypes } from 'react'
import { CardTitle } from 'material-ui/Card'
import { RouteTransition, presets } from 'react-router-transition'
import Container from './Container'


export default class PlanCreation extends React.Component {
  render() {
    const { location } = this.props
    return (
      <Container classNames="center-md">
        <CardTitle 
          title="Register your new plan" 
          subtitle="some subtitle"
        />
      </Container>
    )
  }
}
