import { ReactNode } from 'react'
import { style } from '../lib/style'
import { Widget, WidgetData, WidgetProps } from './Widget'

export const fuck = () => {
  return null
}

interface SingleWidgetProps<T extends WidgetData> extends WidgetProps {
  singleValue: (data: T) => ReactNode
  bottomText?: (data: T) => ReactNode
}

export const SingleWidget = <T extends WidgetData>({
  singleValue,
  bottomText,
  ...props
}: SingleWidgetProps<T>) => (
  <Widget<T> {...props}>
    {({ data }) => (
      <div style={style('flx_c', 'flx_1', { flexBasis: '100%' })}>
        <h1 style={style('flx_1')}>{singleValue(data)}</h1>
        {bottomText && <h5>{bottomText(data)}</h5>}
      </div>
    )}
  </Widget>
)
