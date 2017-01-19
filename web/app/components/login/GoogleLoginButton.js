import React, { PropTypes } from 'react'
import FlatButton from 'material-ui/FlatButton'
import RaisedButton from 'material-ui/RaisedButton'
import { BRAND_GOOGLE } from '../../constants/colors'


export default class FBLoginButton extends React.Component {
  static LABEL = 'Google로 간편하게 로그인';

  render() {
    const { ...restProps } = this.props
    const statusIcon =  (
      <i 
        style={{color: 'white'}} 
        className='fa fa-lg fa-google'>
      </i>
    )

    return (
      <RaisedButton
        label={this.constructor.LABEL}
        labelPosition="after"
        labelStyle={{color: 'white'}}
        backgroundColor={BRAND_GOOGLE}
        {...restProps}
      >
        {statusIcon}
      </RaisedButton>
    )
  }
}
