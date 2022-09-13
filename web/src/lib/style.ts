const createStyles = <T extends Record<string, React.CSSProperties>>(styles: T) => styles

const s = createStyles({
  flx_r: {
    display: 'flex',
    flexDirection: 'row',
  },
  flx_c: {
    display: 'flex',
    flexDirection: 'column',
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
