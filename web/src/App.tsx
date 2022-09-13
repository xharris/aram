import React, { useEffect, useState } from 'react'
import { api } from './lib/api'
import debugModule from 'debug'
import { useSummoner } from './lib/summoner'
import { style } from './lib/style'
import { useStat } from './lib/stat'

localStorage.debug = process.env.REACT_APP_DEBUG

const debug = debugModule('app:app')

const getSummonerCtrlr = new AbortController()

const App = () => {
  const [value, setValue] = useState<string>()
  const [name, setName] = useState<string>()
  const { data: summoner, error, isFetching } = useSummoner({ name })
  const { data: top5, isFetching: fetchingFaveFive } = useStat({
    key: ['top5Champs', summoner?.id],
    url: summoner ? `champions/${summoner.name}/top/5` : undefined,
  })

  return (
    <div style={{ padding: '3rem' }}>
      <div>
        <input placeholder="Summoner name" onChange={(e) => setValue(e.target.value)} />
        <button
          onClick={() => {
            debug('get %s', value)
            setName(value)
          }}
        >
          Go
        </button>
      </div>
      <div>
        <p style={{ color: '#B71C1C' }}>{error?.message}</p>
        {isFetching && <p>Retrieving...</p>}
      </div>
      {summoner && (
        <div>
          <div style={style('flx_r', { gap: 10 })}>
            <img
              style={{
                width: 80,
                height: 80,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                borderRadius: '100%',
                backgroundImage: `url(http://ddragon.leagueoflegends.com/cdn/12.17.1/img/profileicon/${summoner.profileIconId}.png)`,
              }}
            />
            <h2>{summoner.name}</h2>
          </div>
          <div>
            <h3>Your favorite 5</h3>
            {!fetchingFaveFive && top5 ? (
              <>
                {top5.map(
                  (champStat: {
                    _id: React.Key | null | undefined
                    championName: any
                    count: any
                  }) => (
                    <p key={champStat._id}>{`${champStat.championName} (${champStat.count})`}</p>
                  )
                )}
              </>
            ) : (
              <>
                <p>Loading...</p>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default App
