import React, { PropTypes } from 'react'
import FlatButton from 'material-ui/FlatButton'


export default class SignupButton extends React.Component {
  static propTypes = {
    isRegistering: PropTypes.bool.isRequired
  };

  static defaultProps = {
    isRegistering: false,
    primary: true,
  };

  static LABEL = 'Signup to Anchor';

  render() {
    const { isRegistering, ...restProps } = this.props
    const statusIcon = isRegistering ?
      <i className='fa fa-lg fa-spinner fa-spin'></i> :
      <i className='fa fa-lg fa-anchor'></i>

    return (
      <FlatButton
        primary
        label={this.constructor.LABEL}
        labelPosition="after"
        {...restProps}
      >
        {statusIcon}
      </FlatButton>
    )
  }
}
