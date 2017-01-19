import React, { PropTypes } from 'react'
import FlatButton from 'material-ui/FlatButton'
import RaisedButton from 'material-ui/RaisedButton'
import { BRAND_FB } from '../../constants/colors'


export default class FBLoginButton extends React.Component {
  static LABEL = 'Facebook으로 간편하게 로그인';

  render() {
    const { ...restProps } = this.props
    const statusIcon =  (
      <i 
        style={{color: 'white'}} 
        className='fa fa-lg fa-facebook-official'>
      </i>
    )

    return (
      <RaisedButton
        label={this.constructor.LABEL}
        labelPosition="after"
        labelStyle={{color: 'white'}}
        backgroundColor={BRAND_FB}
        {...restProps}
      >
        {statusIcon}
      </RaisedButton>
    )
  }
}
