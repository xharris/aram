import { TableWidget } from '../component/TableWidget'
import { style } from '../lib/style'
import { Image } from '../component/Image'
import { championSquare } from '../lib/ddragon'

interface TableWidgetData {
  _id: number
  championName: string
  win: number
  lose: number
  total: number
}

interface VilliansProps {
  summoner?: Aram.Riot.Summoner
}

export const Villians = ({ summoner }: VilliansProps) => {
  return (
    <TableWidget<TableWidgetData>
      title="Villians"
      rowKey="_id"
      stat={{
        key: ['villians', summoner?.id],
        url: summoner ? `champions/${summoner.name}/history` : undefined,
      }}
      pipeline={(data) => {
        const total = Math.max(...data.map((v) => v.total))
        const avg = data.reduce((sum, v) => sum + v.total, 0) / data.length
        const range = [Math.min(...data.map((v) => v.total)), Math.max(...data.map((v) => v.total))]

        data.forEach((b) => {
          console.log(
            JSON.stringify({
              champion: b.championName,
              rate: b.lose / b.total,
              play: b.total / total,
            })
          )
        })

        const weight = 80
        const playsThreshold = 0.4

        console.log(avg, range, (range[1] - range[0]) * playsThreshold + range[0])

        // prettier-ignore
        return data
        .filter((v) => v.total >= (range[1] - range[0]) * playsThreshold + range[0])
        .sort(
          (a, b) => 
            (b.lose / b.total) - (a.lose / a.total)
            // (((b.lose / b.total) * weight) + ((b.total / total) * (100 - weight))) - 
            // (((a.lose / a.total) * weight) + ((a.total / total) * (100 - weight)))
        )
      }}
      limit={5}
      cells={{
        icon: {
          header: '',
          render: (value: TableWidgetData) => (
            <div style={style('flx')}>
              <Image
                style={{
                  width: 20,
                  height: 20,
                }}
                src={championSquare(value.championName)}
              />
            </div>
          ),
        },
        championName: {
          header: 'Champion',
          render: (value: string) => value,
        },
        lossRate: {
          header: 'Loss Rate',
          render: (value: TableWidgetData) =>
            `${Math.floor((value.lose / value.total) * 100)}% (${value.total})`,
        },
      }}
    />
  )
}
