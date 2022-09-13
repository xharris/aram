import React, { useState } from 'react'
import { api } from './lib/api'
import debugModule from 'debug'

const debug = debugModule('app')

function App() {
  const [summonerName, setSummonerName] = useState('')
  return (
    <div>
      <input placeholder="Summoner name" onChange={(e) => setSummonerName(e.target.value)} />
      <button
        onClick={() => {
          debug('get %s', summonerName)
          api
            .get(`summoner/${summonerName}`)
            .then((res) => {
              if (res.data) {
                debug('summoner %o', res.data)
              }
            })
            .catch((err) => debug('ERR get summoner %s: %o', summonerName, err))
        }}
      >
        Go
      </button>
    </div>
  )
}

export default App
