// import { Widget } from "../component/TableWidget"

import moment from 'moment'
import { SingleWidget } from '../component/SingleWidget'

interface WidgetData {
  count: number
  start: number
}

interface MatchCountProps {
  summoner?: Aram.Riot.Summoner
}

export const MatchCount = ({ summoner }: MatchCountProps) => (
  <SingleWidget<WidgetData>
    title="Conquests"
    stat={{
      key: ['matchCount', summoner?.name],
      url: summoner ? `match/${summoner.name}/count` : undefined,
    }}
    singleValue={(data) => data.count}
    bottomText={(data) => (
      <div style={{ fontStyle: 'italic', opacity: 0.5 }}>
        <span style={{ fontSize: '0.8rem' }}>{`How many arams you've played`}</span>
        <br />
        <span style={{ fontSize: '0.6rem' }}>{`(since ${moment(data.start).format(
          "MMM D 'YY"
        )})`}</span>
      </div>
    )}
  />
)
