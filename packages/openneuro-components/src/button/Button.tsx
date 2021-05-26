import React from 'react'
import './button.scss'

export interface ButtonProps {
  primary?: boolean
  secondary?: boolean
  backgroundColor?: string
  size?: 'xsmall' | 'small' | 'medium' | 'large'
  label?: string
  disabled?: boolean
  onClick?: () => void
  navbar?: boolean
  icon?: string
  color?: string
  imgSrc?: string
  iconSize?: string
  className?: string
  children: React.ReactNode
}

/**
 * Primary UI component for user interaction
 */
export const Button: React.FC<ButtonProps> = ({
  primary,
  size = 'medium',
  backgroundColor,
  label,
  navbar = false,
  icon,
  secondary,
  color,
  imgSrc,
  iconSize,
  className,
  children,
  disabled,
  ...props
}) => {
  const mode =
    primary && !navbar
      ? 'on-button--primary'
      : secondary && !navbar
      ? 'on-button--secondary'
      : !navbar
      ? 'on-no-background'
      : 'on-button--navbar'
  const iconWithText =
    icon && label ? 'icon-text' : imgSrc && label ? 'img-icon-text' : null
  const fontIcon = icon ? (
    <i style={{ fontSize: iconSize }} className={icon}></i>
  ) : null
  const imgIcon = imgSrc ? (
    <img style={{ width: iconSize }} src={imgSrc} alt="" />
  ) : null

  return (
    <button
      disabled={disabled}
      role="button"
      type="button"
      className={[
        'on-button',
        `on-button--${size}`,
        mode,
        iconWithText,
        `${className}`,
      ].join(' ')}
      style={{ backgroundColor, color }}
      {...props}>
      {imgIcon}
      {fontIcon}
      {label}
      {children}
    </button>
  )
}
