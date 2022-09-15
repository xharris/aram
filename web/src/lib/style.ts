const createStyles = <T extends Record<string, React.CSSProperties>>(styles: T) => styles

const s = createStyles({
  fill: {
    width: '100%',
    height: '100%',
  },
  flx: {
    display: 'flex',
  },
  flx_1: {
    flex: 1,
  },
  flx_0: {
    flex: 0,
  },
  flx_r: {
    display: 'flex',
    flexDirection: 'row',
  },
  flx_c: {
    display: 'flex',
    flexDirection: 'column',
  },
  flx_in: {
    display: 'inline-flex',
  },
  h: {
    margin: 0,
  },
  card: {
    backgroundColor: '#FAFAFA',
    borderRadius: 10,
    padding: '1rem',
    boxShadow: '0px 0px 6px -3px #263238',
    boxSizing: 'border-box',
    // width: 400,
    // height: 250,
  },
  ai_c: {
    display: 'flex',
    alignItems: 'center',
  },
  ai_fs: {
    display: 'flex',
    alignItems: 'flex-start',
  },
  ai_fe: {
    display: 'flex',
    alignItems: 'flex-end',
  },
  jc_c: {
    display: 'flex',
    justifyContent: 'center',
  },
  jc_fs: {
    display: 'flex',
    justifyContent: 'flex-start',
  },
  jc_fe: {
    display: 'flex',
    justifyContent: 'flex-end',
  },
})

export const style = (...names: (keyof typeof s | React.CSSProperties)[]) =>
  names.reduce<React.CSSProperties>(
    (obj, name) => ({
      ...obj,
      ...(typeof name === 'string' ? (s[name] as React.CSSProperties) : name),
    }),
    {}
  )
