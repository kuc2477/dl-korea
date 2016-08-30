import React from 'react'
import injectTapEventPlugin from 'react-tap-event-plugin'
import { render } from 'react-dom'
import { Provider } from 'react-redux'

import router from './router'
import store from './store'
import DevTools from './components/dev/DevTools'


// inject tap event plugin
injectTapEventPlugin()

// render app after dom content load
document.addEventListener('DOMContentLoaded', () => {
  render(
    <Provider store={store} >
      <div className="full-height">
        {router}
        <DevTools />
      </div>
    </Provider>,
    document.getElementById('root')
  )
})
