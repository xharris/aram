import { Image } from '../component/Image'
import { Widget } from '../component/Widget'
import { championSquare } from '../lib/ddragon'
import { style } from '../lib/style'

interface WidgetData {
  _id: number
  championName: string
  count: number
}

interface FaveFiveProps {
  summoner: Aram.Riot.Summoner
}

export const FaveFive = ({ summoner }: FaveFiveProps) => {
  return (
    <Widget<WidgetData>
      title="Fave Five"
      rowKey="_id"
      stat={{
        key: ['top5Champs', summoner?.id],
        url: summoner ? `champions/${summoner.name}/top/5` : undefined,
      }}
      cells={{
        icon: {
          header: '',
          render: (value: WidgetData) => (
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
        count: {
          header: '# of Games',
          render: (value: number) => value,
        },
      }}
    />
  )
}
