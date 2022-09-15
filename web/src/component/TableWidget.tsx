import { ReactNode } from 'react'
import { useStat } from '../lib/stat'
import { Widget, WidgetData, WidgetProps } from './Widget'

interface TableWidgetProps<T extends WidgetData> extends WidgetProps {
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
  pipeline?: (data: T[]) => T[]
  limit?: number
}

export const TableWidget = <T extends WidgetData>({
  title,
  stat,
  rowKey,
  cells,
  pipeline,
  limit,
}: TableWidgetProps<T>) => (
  <Widget<T[]> title={title} stat={stat}>
    {({ data }) => (
      <table>
        <thead>
          <tr>
            {Object.keys(cells).map((header) => (
              <th key={header}>{cells[header]?.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {(pipeline ? pipeline(data) : data).slice(0, limit ?? data.length).map((row) => (
            <tr key={row[rowKey]}>
              {Object.keys(cells).map((header) => (
                <td key={row[header] ?? header}>{cells[header]?.render(row[header] ?? row)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    )}
  </Widget>
)
