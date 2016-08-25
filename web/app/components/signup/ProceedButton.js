import React, { PropTypes } from 'react'
import FlatButton from 'material-ui/FlatButton'

export default class ProceedButton extends React.Component {
  static LABEL = 'PROCEED TO NEXT STEP';

  render() {
    const statusIcon = <i className='material-icons fa fa-lg'>arrow_forward</i>

    return (
      <FlatButton
        primary
        label={this.constructor.LABEL}
        labelPosition="after"
        {...this.props}
      >
        {statusIcon}
      </FlatButton>
    )
  }
 }
