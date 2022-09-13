import { useQuery, QueryKey } from '@tanstack/react-query'
import debugModule from 'debug'
import { api } from './api'

const debug = debugModule('app:stat')

export const useStat = ({ key, url }: { key: QueryKey; url?: string }) => {
  const query = useQuery<any, Error>(
    key,
    () => {
      if (url) {
        debug('start stat %o %o', key, url)
        return api.get(url).then((res) => {
          debug('done stat %o %o', key, res.data)
          return res.data
        })
      }
    },
    {
      enabled: !!url,
      refetchOnWindowFocus: false,
    }
  )

  return {
    ...query,
  }
}
