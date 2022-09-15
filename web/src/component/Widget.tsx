import { ReactNode } from 'react'
import { useStat, UseStatProps } from '../lib/stat'
import { style } from '../lib/style'

export interface WidgetProps {
  title: string
  stat: UseStatProps
}

export type WidgetData = Record<string, any>

interface WidgetContainerProps<T extends WidgetData> {
  title: string
  stat: UseStatProps
  children: (props: { data: T }) => ReactNode
}

export const Widget = <T extends WidgetData>({
  title,
  stat,
  children,
}: WidgetContainerProps<T>) => {
  const { data, isFetching } = useStat<T>(stat)

  return (
    <div style={style('card', 'flx_c')}>
      <h4 style={style('h', { textTransform: 'uppercase' })}>{title}</h4>
      <div style={style('fill', 'ai_c', 'jc_c')}>
        {!isFetching && data ? children({ data }) : <p>Loading...</p>}
      </div>
    </div>
  )
}
