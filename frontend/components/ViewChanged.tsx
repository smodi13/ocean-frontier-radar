'use client';

import { useInView, usePrefersReducedMotion } from '@/lib/motion';

interface Story { id: string; title: string; direction: string; steps: string[] }

/**
 * Each story is a sequence of research steps that moved the view in one
 * direction. The connecting line draws downward and the steps arrive in order,
 * because the order is the argument: what was believed, what was checked, what
 * that changed.
 */
export function ViewChangedStory({ story }: { story: Story }) {
  const reduced = usePrefersReducedMotion();
  const [ref, inView] = useInView<HTMLDivElement>();
  const show = reduced || inView;
  const improved = story.direction === 'strengthened_company';
  const stepMs = 260;

  return (
    <div ref={ref} className="card p-5">
      <div className="flex flex-wrap items-center gap-2">
        <span className={`chip ${improved ? 'chip-moss' : 'chip-rust'}`}>
          {improved ? 'View improved' : 'View weakened'}
        </span>
        <h3 className="h3 text-[15px]">{story.title}</h3>
      </div>

      <ol className="relative mt-4 space-y-3 pl-6">
        {/* The rail is drawn, not just present. */}
        <span
          aria-hidden
          className={`absolute left-[3px] top-1.5 w-px origin-top ${improved ? 'bg-moss/40' : 'bg-rust/40'}`}
          style={{
            bottom: '0.5rem',
            transform: show ? 'scaleY(1)' : 'scaleY(0)',
            transition: reduced
              ? 'none'
              : `transform ${story.steps.length * stepMs + 260}ms cubic-bezier(.22,.61,.36,1)`,
          }}
        />
        {story.steps.map((step, i) => (
          <li
            key={i}
            className="relative"
            style={
              reduced
                ? undefined
                : {
                    opacity: show ? 1 : 0,
                    transform: show ? 'none' : 'translateY(6px)',
                    transition: `opacity 420ms ease ${i * stepMs}ms, transform 420ms ease ${i * stepMs}ms`,
                  }
            }
          >
            <span
              aria-hidden
              className={`absolute -left-6 top-[7px] h-[7px] w-[7px] rounded-full ring-4 ring-paper-card ${
                improved ? 'bg-moss' : 'bg-rust'
              }`}
            />
            <span className="body text-[13.5px]">{step}</span>
          </li>
        ))}
      </ol>
    </div>
  );
}
