import { useQuery, QueryKey, UseQueryResult } from '@tanstack/react-query'
import debugModule from 'debug'
import { api } from './api'

const debug = debugModule('app:stat')

export interface UseStatProps {
  key: QueryKey
  url?: string
}

export const useStat = <T = any>({ key, url }: UseStatProps) => {
  const query = useQuery<T[] | undefined, Error>(
    key,
    () => {
      if (url) {
        debug('start stat %o %o', key, url)
        return api.get<T[]>(url).then((res) => {
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
