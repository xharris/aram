import { useState } from 'react'
import './app.scss'
import './style.scss'
import debugModule from 'debug'
import { useSummoner } from './lib/summoner'
import { style } from './lib/style'
import { FaveFive } from './widgets/faveFive'
import { Image } from './component/Image'
import { summonerProfileIcon } from './lib/ddragon'

localStorage.debug = process.env.REACT_APP_DEBUG

const debug = debugModule('app:app')

const App = () => {
  const [value, setValue] = useState<string>()
  const [name, setName] = useState<string>()
  const { data: summoner, error, isFetching } = useSummoner({ name })

  return (
    <div className="app" style={style('flx_c', { padding: '3rem', gap: 20 })}>
      <div style={style('flx_r', 'ai_c', { gap: 5 })}>
        <input
          name="summonerName"
          placeholder="Summoner name"
          onChange={(e) => setValue(e.target.value)}
        />
        <button
          onClick={() => {
            debug('get %s', value)
            setName(value)
          }}
        >
          Go
        </button>
      </div>
      {(error || isFetching) && (
        <div>
          <p style={{ color: '#B71C1C' }}>{error?.message}</p>
          {isFetching && <p>Retrieving...</p>}
        </div>
      )}
      {summoner && (
        <>
          <div style={style('flx_r', 'ai_c', { gap: 20 })}>
            <Image
              style={{
                width: 80,
                height: 80,
              }}
              src={summonerProfileIcon(summoner.profileIconId)}
            />
            <h2>{summoner.name}</h2>
          </div>
          <div style={style('flx_in')}>
            <FaveFive summoner={summoner} />
          </div>
        </>
      )}
    </div>
  )
}

export default App
