import { ReactNode } from 'react'
import { useStat, UseStatProps } from '../lib/stat'
import { style } from '../lib/style'

interface WidgetProps<T extends Record<string, any>> {
  title: string
  stat: UseStatProps
  rowKey: keyof T
  cells: Partial<
    Record<
      keyof T | string,
      {
        header: string
        render: (value: any) => ReactNode
      }
    >
  >
}

export const Widget = <T extends Record<string, any>>({
  title,
  stat,
  rowKey,
  cells,
}: WidgetProps<T>) => {
  const { data, isFetching } = useStat<T>(stat)

  return (
    <div style={style('card', 'flx_c')}>
      <h4 style={style('h', { textTransform: 'uppercase' })}>{title}</h4>
      <div style={style('fill', 'ai_c', 'jc_c')}>
        {!isFetching && data ? (
          <table>
            <thead>
              <tr>
                {Object.keys(cells).map((header) => (
                  <th key={header}>{cells[header]?.header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data?.map((row) => (
                <tr key={row[rowKey]}>
                  {Object.keys(cells).map((header) => (
                    <td key={row[header] ?? header}>{cells[header]?.render(row[header] ?? row)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </div>
  )
}
