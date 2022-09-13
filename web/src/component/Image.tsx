import { ImgHTMLAttributes } from 'react'

interface ImageProps extends ImgHTMLAttributes<HTMLImageElement> {}

export const Image = ({ src, style, ...props }: ImageProps) => (
  <img
    {...props}
    style={{
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      borderRadius: '100%',
      backgroundImage: `url(${src})`,
      ...style,
    }}
  />
)
