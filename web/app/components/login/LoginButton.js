import React, { PropTypes } from 'react'
import FlatButton from 'material-ui/FlatButton'


export default class LoginButton extends React.Component {
  static propTypes = {
    isAuthenticating: PropTypes.bool.isRequired
  };

  static defaultProps = {
    isAuthenticating: false,
    primary: true,
  };

  static LABEL = 'Login to Anchor';

  render() {
    const { isAuthenticating, ...restProps } = this.props
    const statusIcon = isAuthenticating ?
      <i className='fa fa-lg fa-spinner fa-spin'></i> :
      <i className='fa fa-lg fa-check'></i>

    return (
      <FlatButton
        secondary={true}
        label={this.constructor.LABEL}
        labelPosition="after"
        {...restProps}
      >
        {statusIcon}
      </FlatButton>
    )
  }
}
