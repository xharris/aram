import { useQuery } from '@tanstack/react-query'
import { api } from './api'
import debugModule from 'debug'

const debug = debugModule('app:summoner')

export const useSummoner = ({ name }: { name?: string }) => {
  const query = useQuery<Aram.Riot.Summoner, Error>(
    ['summoner', { name }],
    () =>
      api
        .get(`summoner/${name}`)
        .then((res) => {
          if (res.data) {
            debug('summoner %o', res.data)
          }
          return res.data
        })
        .catch((err) => {
          debug('ERR get summoner %s: %o', name, err)
          if (err.response) {
            if (err.response.status === 500) {
              throw new Error('Server had an oopsie. Try again later!')
            }
            if (err.response.status === 404) {
              throw new Error('Summoner not found')
            }
          }
        }),
    { enabled: !!name, refetchOnWindowFocus: false }
  )

  return {
    ...query,
  }
}
