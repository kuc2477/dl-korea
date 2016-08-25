'use strict'

// import all test specs
const testContext = require.context('./tests', true, /\.spec\.jsx?$/)
testContext.keys().forEach(testContext)
