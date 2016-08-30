import React from 'react'


export default class Container extends React.Component {
  render() {
    const { classNames, ...props } = this.props
    const className = `${classNames} page-container row`
    return (
      <div className={className} {...props}>
        {this.props.children}
      </div>
    )
  }
}
