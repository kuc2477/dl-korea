import _ from 'lodash'
import React, { PropTypes } from 'react'
import AppBar from 'material-ui/AppBar'
import { Tabs, Tab } from 'material-ui/Tabs'
import { INDICATOR } from '../../constants/colors'
import { UserPropType } from '../../constants/types'
import { POSTS, PROFILE, LOGIN, LOGOUT } from '../../constants/routes'
import { logout } from '../../actions/auth'


export default class Nav extends React.Component {
  static propTypes = {
    user: UserPropType,
    title: PropTypes.string.isRequired,
    // need dispatcher to dispatch logout action
    dispatch: PropTypes.func.isRequired,
    location: PropTypes.object.isRequired
  };

  static contextTypes = {
    router: PropTypes.object.isRequired
  };

  static defaultProps = {
    title: 'Deep Learning Korea'
  };

  constructor(props) {
    super(props)
    this.state = { tabIndex: 0 }
  }

  componentWillMount() {
    this.setState({ tabIndex: this._getSelectedIndex() })
  }

  componentWillReceiveProps() {
    if (this.state.tabIndex !== this._getSelectedIndex()) {
      this.setState({ tabIndex: this._getSelectedIndex() })
    }
  }

  static ROUTES = [[LOGIN], [PROFILE, LOGOUT,]];
  static APP_BAR_STYLE = { position: 'fixed' };
  static TAB_INK_STYLE = { color: INDICATOR };
  static TAB_ITEM_STYLE = { marginRight: 120 };

  _onTabActive(tab) {
    // run logout action if activated tab is logout tab
    if (tab.props.label === LOGOUT.label ||
      tab.props.label === LOGIN.label) {
      const { dispatch } = this.props
      dispatch(logout(this.context.router))
      return
    }

    // otherwise navigate to related route
    this.context.router.push(tab.props.path)
    this.setState({ tabIndex: this._getSelectedIndex() })
  }

  _getTabRoutes() {
    const { user } = this.props
    return _(this.constructor.ROUTES).flatten().filter(route => (
      (!route.onlyVisibleToAnonymous && !route.onlyVisibleToAuthenticated) ||
        (route.onlyVisibleToAuthenticated && user) ||
          (route.onlyVisibleToAnonymous && !user)
    )).value()
  }

  _getSelectedIndex() {
    const location = this.props.location
    const router = this.context.router
    const routes = this._getTabRoutes()
    return _.findIndex(
      routes, route => route.path && (
        router.isActive(route.path) || 
        _.startsWith(location.pathname, route.path)
    ))
  }


  render() {
    const tabItems = this._getTabRoutes().map(
      (route, index) =>
      <Tab
        key={index}
        value={JSON.stringify(index)}
        label={route.label}
        path={route.path}
        link={route.link}
        onActive={::this._onTabActive}
      />
    )

    const tabs = (
      <Tabs
        value={JSON.stringify(this.state.tabIndex)}
        tabItemContainerStyle={this.constructor.TAB_ITEM_STYLE}
        inkBarStyle={this.constructor.TAB_INK_STYLE}
      >
        {tabItems}
      </Tabs>
    )

    const icon = (
      <i
        style={{ margin: 8, color: 'white' }}
        className="fa fa-2x fa-braille clickable"
      >
      </i>
    )

    const goHome = () => {this.context.router.push('/')}

    return (
      <AppBar
        className="draggable"
        style={this.constructor.APP_BAR_STYLE}
        title={this.props.title}
        iconElementLeft={icon}
        iconElementRight={tabs}
        onLeftIconButtonTouchTap={goHome}
        onTitleTouchTap={goHome}
        titleStyle={{cursor: 'pointer'}}
      />
    )
  }
}
